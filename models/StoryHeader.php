<?php

namespace datagutten\InducksORM\models;

use Doctrine\DBAL\Types\Types;
use Doctrine\ORM\Mapping as ORM;
use Doctrine\ORM\PersistentCollection;


#[ORM\Table(name: 'inducks_storyheader')]
#[ORM\Entity(readOnly: true)]
/**
 * A group of stories (or movies) that have codes starting with the same letter(s).
 */
class StoryHeader
{
    public function __construct(
        #[ORM\Id, ORM\Column(type: Types::STRING)]
        private string $storyheadercode,
        #[ORM\Column(type: Types::INTEGER)]
        private int    $level,
    )
    {
    }

    #[ORM\Column(type: Types::STRING)]
    private string $title;

    #[ORM\Column(type: Types::STRING)]
    private string $storyheadercomment;

    #[ORM\ManyToOne(targetEntity: Country::class, inversedBy: 'storyheaders')]
    #[ORM\JoinColumn(name: 'countrycode', referencedColumnName: 'countrycode')]
    private Country $country;

/*    #[ORM\ManyToOne(targetEntity: Story::class)]
    #[ORM\JoinColumn(name: 'storyheadercode', referencedColumnName: 'storyheadercode')]
    private PersistentCollection $stories;*/

    /*    #[ORM\ManyToOne(targetEntity: Story::class, inversedBy: 'headers')]
        #[ORM\JoinColumn(name: 'storyheadercode', referencedColumnName: 'storyheadercode')]*/
    //private PersistentCollection $stories;

    public function getStoryHeaderCode(): string
    {
        return $this->storyheadercode;
    }

    /**
     * 0, 1, or 2 (or 3, only for movies)
     * @return int
     */
    public function getLevel(): int
    {
        return $this->level;
    }

    public function getTitle(): string
    {
        return $this->title;
    }

    /**
     * Remarks about the group of stories
     * @return string
     */
    public function getStoryHeaderComment(): string
    {
        return $this->storyheadercomment;
    }

    /**
     * Country where the stories are produced
     * @return Country
     */
    public function getCountry(): Country
    {
        return $this->country;
    }

    /**
     * @return PersistentCollection<int, Story>
     */
    public function getStories(): PersistentCollection
    {
        return $this->stories;
    }
}