<?php

namespace datagutten\InducksORM\models;

use Doctrine\ORM\Mapping as ORM;


/**
 * EntryUrl
 *
 *
 * @author datagutten
 */
#[ORM\Table(name: 'inducks_characterurl_custom')]
#[ORM\Entity(readOnly: false)]
class CharacterUrl
{
    #[ORM\Column]
    private string $charactercode;

    #[ORM\ManyToOne(targetEntity: Character::class, inversedBy: 'urls')]
    #[ORM\JoinColumn(name: 'charactercode', referencedColumnName: 'charactercode')]
    #[ORM\Id]
    private Character $character;

    #[ORM\Column]
    private string $sitecode;

    #[ORM\ManyToOne(targetEntity: Site::class)]
    #[ORM\JoinColumn(name: 'sitecode', referencedColumnName: 'sitecode')]
    #[ORM\Id]
    private Site $site;

    #[ORM\Column]
    #[ORM\Id]
    private string $url;

    #[ORM\Column(type: 'string')]
    private string $storycode;


    public function generateUrl(): string
    {
        //return $this->site->getURLBase() . $this->url;
        $urlbase = 'https://outducks.org/webusers/';
        return sprintf('https://inducks.org/hr.php?normalsize=1&image=%s', urlencode($urlbase)) . $this->url;
    }

    public function getCharacterCode(): string
    {
        return $this->charactercode;
    }

    /**
     * Get entry object
     * @return Character
     */
    public function getCharacter(): Character
    {
        return $this->character;
    }

    public function getSiteCode(): string
    {
        return $this->sitecode;
    }

    /**
     * Get site object
     * @return Site
     */
    public function getSite(): Site
    {
        return $this->site;
    }

    /**
     * Get relative URL
     * @return string
     */
    public function getUrl(): string
    {
        return $this->url;
    }

    /**
     * @param string $charactercode
     */
    public function setCharacterCode(string $charactercode): void
    {
        $this->charactercode = $charactercode;
    }

    /**
     * @param string $sitecode
     */
    public function setSiteCode(string $sitecode): void
    {
        $this->sitecode = $sitecode;
    }

    public function setUrl(string $url): void
    {
        $url = str_replace('hr.php?normalsize=1&image=https://outducks.org/webusers/', '', $url);
        $this->url = $url;
    }

    /**
     * @param Character $character
     */
    public function setCharacter(Character $character): void
    {
        $this->character = $character;
        $this->charactercode = $character->getCharactercode();
    }

    /**
     * @param Site $site
     */
    public function setSite(Site $site): void
    {
        $this->site = $site;
        $this->sitecode = $site->getSiteCode();
    }

    /**
     * @return string
     */
    public function getStoryCode(): string
    {
        return $this->storycode;
    }

    /**
     * @param string $storyCode
     */
    public function setStoryCode(string $storyCode): void
    {
        $this->storycode = $storyCode;
    }
}
