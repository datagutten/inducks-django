<?php

namespace datagutten\InducksORM\models;

use DateTimeImmutable;
use Doctrine\ORM\Mapping as ORM;
use Doctrine\ORM\PersistentCollection;
use Exception;


/**
 * Person
 *
 *
 * @author dromanin
 */
#[ORM\Table(name: 'inducks_person')]
#[ORM\Entity(readOnly: true)]
class Person
{
    #[ORM\Column(type: 'string')]
    #[ORM\Id]
    private string $personcode;

    #[ORM\Column(type: 'string')]
    private string $nationalitycountrycode;

    #[ORM\ManyToOne(targetEntity: Country::class)]
    #[ORM\JoinColumn(name: 'nationalitycountrycode', referencedColumnName: 'countrycode')]
    private Country $nationality;

    #[ORM\Column(type: 'string')]
    private string $fullname;

    #[ORM\Column(type: 'string')]
    private string $official;

    #[ORM\Column(type: 'string')]
    private string $personcomment;

    #[ORM\Column(type: 'string')]
    private string $unknownstudiomember;

    #[ORM\Column(type: 'string')]
    private string $isfake;

    #[ORM\Column(type: 'integer')]
    private int $numberofindexedissues;

    #[ORM\Column(type: 'string')]
    private string $birthname;

    #[ORM\Column(type: 'string')]
    private string $borndate;

    #[ORM\Column(type: 'string')]
    private string $bornplace;

    #[ORM\Column(type: 'string')]
    private string $deceaseddate;

    #[ORM\Column(type: 'string')]
    private string $deceasedplace;

    #[ORM\Column(type: 'string')]
    private string $education;

    #[ORM\Column(type: 'string')]
    private string $moviestext;

    #[ORM\Column(type: 'string')]
    private string $comicstext;

    #[ORM\Column(type: 'string')]
    private string $othertext;

    #[ORM\Column(type: 'string')]
    private string $photofilename;

    #[ORM\Column(type: 'string')]
    private string $photocomment;

    #[ORM\Column(type: 'string')]
    private string $photosource;

    #[ORM\Column(type: 'string')]
    private string $personrefs;

    #[ORM\OneToMany(mappedBy: 'person', targetEntity: EntryJob::class)]
    private PersistentCollection $entryJobs;

    #[ORM\OneToMany(mappedBy: 'person', targetEntity: StoryJob::class)]
    private PersistentCollection $storyJobs;

    #[ORM\OneToMany(mappedBy: 'person', targetEntity: IssueJob::class)]
    private PersistentCollection $issueJobs;

    public function getPersoncode(): string
    {
        return $this->personcode;
    }

    public function getNationalityCountryCode(): string
    {
        return $this->nationalitycountrycode;
    }

    public function getNationality(): Country
    {
        return $this->nationality;
    }

    public function getFullname(): string
    {
        return $this->fullname;
    }

    /**
     * @return PersistentCollection
     */
    public function getEntries(): PersistentCollection
    {
        return $this->entryJobs;
    }

    /**
     * @return PersistentCollection
     */
    public function getStoryJobs(): PersistentCollection
    {
        return $this->storyJobs;
    }

    public function getIssueJobs(): PersistentCollection
    {
        return $this->issueJobs;
    }

    public function getOfficial(): bool
    {
        return $this->official == 'Y';
    }

    /**
     * @return string
     */
    public function getPersonComment(): string
    {
        return $this->personcomment;
    }

    public function getUnknownStudioMember(): bool
    {
        return $this->unknownstudiomember == 'Y';
    }

    public function getIsFake(): bool
    {
        return $this->isfake == 'Y';
    }

    public function getNumberOfIndexedIssues(): int
    {
        return $this->numberofindexedissues;
    }

    public function getBirthName(): string
    {
        return $this->birthname;
    }

    public function getBornDate(): ?DateTimeImmutable
    {
        if (empty($this->borndate))
            return null;
        try
        {
            return new DateTimeImmutable($this->borndate);
        }
        catch (Exception)
        {
            return null;
        }
    }

    public function getBornPlace(): string
    {
        return $this->bornplace;
    }

    public function getDeceasedDate(): ?DateTimeImmutable
    {
        try
        {
            return new DateTimeImmutable($this->deceaseddate);
        }
        catch (Exception)
        {
            return null;
        }
    }

    public function getDeceasedPlace(): string
    {
        return $this->deceasedplace;
    }

    /**
     * @return string
     */
    public function getEducation(): string
    {
        return $this->education;
    }

    /**
     * @return string
     */
    public function getMoviesText(): string
    {
        return $this->moviestext;
    }

    /**
     * @return string
     */
    public function getComicsText(): string
    {
        return $this->comicstext;
    }

    /**
     * @return string
     */
    public function getOtherText(): string
    {
        return $this->othertext;
    }

    /**
     * @return string
     */
    public function getPhotoFilename(): string
    {
        return $this->photofilename;
    }

    /**
     * Photo comment
     * @return string
     */
    public function getPhotoComment(): string
    {
        return $this->photocomment;
    }

    /**
     * @return string
     */
    public function getPhotoSource(): string
    {
        return $this->photosource;
    }

    /**
     * @return string
     */
    public function getPersonRefs(): string
    {
        return $this->personrefs;
    }

    public function __toString(): string
    {
        return $this->fullname;
    }
}
