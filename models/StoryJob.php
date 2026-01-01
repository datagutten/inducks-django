<?php

namespace datagutten\InducksORM\models;

use Doctrine\ORM\EntityNotFoundException;
use Doctrine\ORM\Mapping as ORM;

/**
 * StoryJob
 *
 *
 * @author dromanin
 */
#[ORM\Table(name: 'inducks_storyjob')]
#[ORM\Entity(readOnly: true)]
class StoryJob
{
    #[ORM\ManyToOne(targetEntity: StoryVersion::class, inversedBy: 'jobs')]
    #[ORM\JoinColumn(name: 'storyversioncode', referencedColumnName: 'storyversioncode')]
    #[ORM\Id]
    private StoryVersion $storyversion;

    #[ORM\ManyToOne(targetEntity: Person::class, inversedBy: 'storyjobs')]
    #[ORM\JoinColumn(name: 'personcode', referencedColumnName: 'personcode')]
    #[ORM\Id]
    private Person $person;

    /**
     * Describes the job: p=plot, w=writing, a=art(pencils), i=ink, r=reference, m=maintainer(incharge)
     */
    #[ORM\Column(type: 'string')]
    #[ORM\Id]
    private string $plotwritartink;

    #[ORM\Column(type: 'string')]
    private string $storyjobcomment;

    public function getStoryversion(): StoryVersion
    {
        return $this->storyversion;
    }

    public function getPerson(): Person
    {
        return $this->person;
    }

    public function getPlotwritartink(): string
    {
        return $this->plotwritartink;
    }

    public function getStoryjobcomment(): string
    {
        return $this->storyjobcomment;
    }

    public function getRoleName(): string
    {
        switch ($this->plotwritartink)
        {
            case 'p':
                return 'plot';
            case 'w':
                return 'writer';
            case 'a':
                return 'artist';
            case 'i':
                return 'inker';
            case 'r':
                return 'reference'; // ??
            case 'm':
                return 'maintainer';
        }
        throw new EntityNotFoundException('Invalid role');
    }

}
