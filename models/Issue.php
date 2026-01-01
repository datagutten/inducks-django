<?php

namespace datagutten\InducksORM\models;

use Doctrine\Common\Collections\Collection;
use Doctrine\Common\Collections\Criteria;
use Doctrine\ORM\EntityNotFoundException;
use Doctrine\ORM\Mapping as ORM;
use Doctrine\ORM\PersistentCollection;
use Exception;


#[ORM\Entity(readOnly: true)]
#[ORM\Table(name: 'inducks_issue')]
class Issue
{
    #[ORM\Id]
    #[ORM\Column(type: 'string')]
    private string $issuecode;

    #[ORM\ManyToOne(targetEntity: Publication::class, inversedBy: 'issues')]
    #[ORM\JoinColumn(name: 'publicationcode', referencedColumnName: 'publicationcode')]
    private Publication $publication;

    #[ORM\Column(type: 'string')]
    private string $issuenumber;

    #[ORM\Column(type: 'string')]
    private string $title;

    #[ORM\Column(type: 'string')]
    private string $size;

    #[ORM\Column(type: 'string')]
    private string $pages;

    #[ORM\Column(type: 'string')]
    private string $price;

    #[ORM\Column(type: 'string')]
    private string $printrun;

    #[ORM\Column(type: 'string')]
    private string $attached;

    #[ORM\Column(type: 'string')]
    private string $oldestdate;

    #[ORM\Column(type: 'string')]
    private string $issuecomment;

    #[ORM\OneToMany(mappedBy: 'issue', targetEntity: IssueJob::class)]
    private PersistentCollection $jobs;

    /**
     * @var PersistentCollection<int, IssueURL>
     */
    #[ORM\OneToMany(mappedBy: 'issue', targetEntity: IssueUrl::class)]
    private PersistentCollection $urls;

    /**
     * @var PersistentCollection<int, Entry>
     */
    #[ORM\OneToMany(mappedBy: 'issue', targetEntity: Entry::class)]
    #[ORM\OrderBy(['position' => 'ASC'])]
    private PersistentCollection $entries;

    #[ORM\OneToMany(mappedBy: 'issue', targetEntity: IssueDate::class)]
    private PersistentCollection $dates;

    #[ORM\OneToMany(mappedBy: 'issue', targetEntity: PublishingJob::class)]
    private PersistentCollection $publishingJobs;

    #[ORM\OneToMany(mappedBy: 'collected', targetEntity: IssueCollecting::class)]
    private PersistentCollection $collected;

    #[ORM\OneToMany(mappedBy: 'collecting', targetEntity: IssueCollecting::class)]
    private PersistentCollection $collecting;

    function getIssuecode(): string
    {
        return $this->issuecode;
    }

    function getPublication(): Publication
    {
        return $this->publication;
    }

    function getIssuenumber(): string
    {
        return $this->issuenumber;
    }

    function getTitle(): string
    {
        if (empty($this->title))
            return sprintf('%s %s', $this->publication->getTitle(), $this->getIssuenumber());
        else
            return $this->title;
    }

    function getTitleFull(): string
    {
        if (empty($this->title))
            return sprintf('%s %s', $this->publication->getTitle(), $this->getIssuenumber());
        else
            return sprintf('%s %s %s', $this->publication->getTitle(), $this->getIssuenumber(), $this->title);
    }

    function getSize(): string
    {
        return $this->size;
    }

    function getPages(): string
    {
        return $this->pages;
    }

    function getPrice(): string
    {
        return $this->price;
    }

    function getPrintrun(): string
    {
        return $this->printrun;
    }

    function getAttached(): string
    {
        return $this->attached;
    }

    function getOldestdate(): string
    {
        return $this->oldestdate;
    }

    public function getYear(): string
    {
        return substr($this->oldestdate, 0, 4);
    }

    function getIssuecomment(): string
    {
        return $this->issuecomment;
    }

    public function getJobs(string $type): Collection
    {
        $criteria = Criteria::create()->where(Criteria::expr()->eq('inxtransletcol', $type));
        return $this->jobs->matching($criteria);
    }

    /**
     * @return PersistentCollection<int, Entry>
     */
    function getEntries(): PersistentCollection
    {
        return $this->entries;
    }

    public function getThumbnailUrl(): string
    {
        if ($this->urls->count() > 0)
        {
            return $this->urls->first()->generateUrl();
        }
        if ($this->entries->count() > 0)
        {
            return $this->entries->first()->getThumbnailUrl();
        }
        throw new EntityNotFoundException('Thumbnail URL not found');
    }

    /**
     * @return Story[]
     * @throws Exception
     */
    public function getStories(): array
    {
        $stories = [];
        /** @var Entry $entry */
        foreach ($this->entries->getIterator() as $entry)
        {
            try
            {
                $stories[] = $entry->getStoryversion()->getStory();
            }
            catch (EntityNotFoundException)
            {
                continue;
            }
        }
        return $stories;
    }

    public function getURL(): string
    {
        return sprintf('https://inducks.org/issue.php?c=%s', urlencode($this->issuecode));
    }

    /**
     * Get issue URLs
     * @return PersistentCollection<int, IssueUrl>
     */
    public function getUrls(): PersistentCollection
    {
        return $this->urls;
    }

    /**
     * @return IssueJob[]
     */
    public function getIndexers(): array
    {
        $criteria = Criteria::create()->where(Criteria::expr()->eq('inxtransletcol', 'i'));
        $indexers = $this->jobs->matching($criteria);
        return $indexers->getValues();
    }

    public function getTranslators(): Collection
    {
        return $this->getJobs('t');
    }

    public function getDates(): PersistentCollection
    {
        return $this->dates;
    }

    public function getPublishingJobs(): PersistentCollection
    {
        return $this->publishingJobs;
    }

    public function __toString(): string
    {
        return sprintf('%s %d', $this->publication->getTitle(), $this->issuenumber);
    }

    /**
     * Issues collected by this issue
     * @return PersistentCollection
     */
    public function getCollected(): PersistentCollection
    {
        return $this->collected;
    }

    /**
     * Issues collecting this issue
     * @return PersistentCollection
     */
    public function getCollecting(): PersistentCollection
    {
        return $this->collecting;
    }

}
