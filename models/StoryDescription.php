<?php

namespace datagutten\InducksORM\models;

use Doctrine\Common\Collections\Criteria;
use Doctrine\DBAL\Types\Types;
use Doctrine\ORM\EntityNotFoundException;
use Doctrine\ORM\Mapping as ORM;
use Doctrine\ORM\PersistentCollection;


/**
 * Story
 *
 *
 * @author datagutten
 */
#[ORM\Table(name: 'inducks_storydescription')]
#[ORM\Entity(readOnly: true)]
class StoryDescription
{
    public function __construct(
        #[ORM\Id, ORM\Column(type: Types::STRING)]
        private string $storyversioncode,
        #[ORM\Id, ORM\Column(type: Types::STRING)]
        private string $languagecode,
    )
    {
    }

    #[ORM\ManyToOne(targetEntity: StoryVersion::class, inversedBy: 'descriptions')]
    #[ORM\JoinColumn(name: 'storyversioncode', referencedColumnName: 'storyversioncode')]
    private StoryVersion $storyVersion;

    #[ORM\ManyToOne(targetEntity: Language::class)]
    #[ORM\JoinColumn(name: 'languagecode', referencedColumnName: 'languagecode')]
    private Language $language;

    #[ORM\Column(type: Types::STRING)]
    private string $desctext;

    /**
     * @return string
     */
    public function getStoryVersionCode(): string
    {
        return $this->storyversioncode;
    }

    public function getLanguageCode(): string
    {
        return $this->languagecode;
    }

    public function getStoryVersion(): StoryVersion
    {
        return $this->storyVersion;
    }

    public function getLanguage(): Language
    {
        return $this->language;
    }

    /**
     * Get description text
     * @return string
     */
    public function getDescText(): string
    {
        return $this->desctext;
    }
}

