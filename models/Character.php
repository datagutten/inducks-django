<?php

namespace datagutten\InducksORM\models;

use Doctrine\Common\Collections\Criteria;
use Doctrine\ORM\EntityNotFoundException;
use Doctrine\ORM\Mapping as ORM;
use Doctrine\ORM\PersistentCollection;

/**
 * Character
 *
 *
 * @author dromanin
 */
#[ORM\Table(name: 'inducks_character')]
#[ORM\Entity(readOnly: true)]
class Character
{
    #[ORM\Id]
    #[ORM\Column(type: 'string')]
    private string $charactercode;

    #[ORM\Column(type: 'string')]
    private string $charactername;

    #[ORM\Column(type: 'string')]
    private string $official;

    #[ORM\Column(type: 'string')]
    private string $onetime;

    #[ORM\Column(type: 'string')]
    private string $heroonly;

    #[ORM\Column(type: 'string')]
    private string $charactercomment;


    /**
     * @var PersistentCollection<int, CharacterName>
     */
    #[ORM\OneToMany(mappedBy: 'character', targetEntity: CharacterName::class)]
    private PersistentCollection $names;

    /**
     * @var PersistentCollection<int, CharacterUrl>
     */
    #[ORM\OneToMany(mappedBy: 'character', targetEntity: CharacterUrl::class)]
    private PersistentCollection $urls;

    /**
     * @var PersistentCollection<int, EntryCharacterName>
     */
    #[ORM\OneToMany(mappedBy: 'character', targetEntity: EntryCharacterName::class)]
    private PersistentCollection $entryNames;

    #[ORM\OneToMany(mappedBy: 'character', targetEntity: Appearance::class)]
    private PersistentCollection $appearances;

    #[ORM\OneToMany(mappedBy: 'character', targetEntity: UniverseCharacter::class)]
    private PersistentCollection $universes;

    #[ORM\OneToMany(mappedBy: 'characterFrom', targetEntity: CharacterReference::class)]
    private PersistentCollection $referencesFrom;

    #[ORM\OneToMany(mappedBy: 'characterTo', targetEntity: CharacterReference::class)]
    private PersistentCollection $referencesTo;

    #[ORM\OneToMany(mappedBy: 'character', targetEntity: LogoCharacter::class)]
    private PersistentCollection $logos;

    function getCharactercode(): string
    {
        return $this->charactercode;
    }

    function getCharactername(): string
    {
        return $this->charactername;
    }

    function getNames(): PersistentCollection
    {
        return $this->names;
    }

    /**
     * Get character localized name
     * @param string $languageCode Language code
     * @param bool $preferred Get the preferred name
     * @return CharacterName CharacterName object
     * @throws EntityNotFoundException Name not found
     */
    function getLocalizedName(string $languageCode, bool $preferred = true): CharacterName
    {
        $preferred = $preferred ? 'Y' : 'N';
        $names = $this->names->matching(Criteria::create()->
        where(Criteria::expr()->eq('languagecode', $languageCode))->
        andWhere(Criteria::expr()->eq('preferred', $preferred)));
        if (empty($names->first()))
            throw new EntityNotFoundException('Localized name not found');
        return $names->first();
    }

    public function getLocalizedName2($languageCode): ?string
    {
        $criteria = Criteria::create()->where(Criteria::expr()->eq('languagecode', $languageCode));
        $matches = $this->names->matching($criteria);
        if (!empty($matches->count()))
            return $matches->first()->getUniverseName();
        else
            return null;
    }

    public function getOfficial(): bool
    {
        return $this->official == 'Y';
    }

    public function getOnetime(): bool
    {
        return $this->onetime == 'Y';
    }

    public function getHeroOnly(): bool
    {
        return $this->heroonly == 'Y';
    }

    public function getCharacterComment(): string
    {
        return $this->charactercomment;
    }

    public function getEntryNames(): PersistentCollection
    {
        return $this->entryNames;
    }

    /**
     * @return PersistentCollection<int, Appearance>
     */
    public function getAppearances(): PersistentCollection
    {
        return $this->appearances;
    }

    public function getFirstAppearance(): Appearance
    {
        /** @var Appearance $appearance */
        foreach ($this->appearances->getIterator() as $appearance)
        {
            $storyversion = $appearance->getStoryversion();
            $story = $storyversion->getStory();
            try
            {
                $date_obj = $story->getFirstPublicationDate_obj();
            }
            catch (EntityNotFoundException $e)
            {
                continue;
            }
            if (empty($lowest) || $lowest > $date_obj->getTimestamp())
            {
                $lowest = $date_obj->getTimestamp();
                $lowest_app = $appearance;
            }
        }
        return $lowest_app;
    }

    /**
     * @return PersistentCollection<int, UniverseCharacter>
     */
    public function getUniverses(): PersistentCollection
    {
        return $this->universes;
    }

    /**
     * Characters this character refers to
     * @return PersistentCollection<int, CharacterReference>
     */
    public function getReferencesFrom(): PersistentCollection
    {
        return $this->referencesFrom;
    }

    /**
     * Characters that refers to this character
     * @return PersistentCollection<int, CharacterReference>
     */
    public function getReferencesTo(): PersistentCollection
    {
        return $this->referencesTo;
    }

    public function getLogos(): PersistentCollection
    {
        return $this->logos;
    }

    public function __toString(): string
    {
        return $this->charactername;
    }

    /**
     * @return PersistentCollection<int, CharacterUrl>
     */
    public function getUrls(): PersistentCollection
    {
        return $this->urls;
    }
}
