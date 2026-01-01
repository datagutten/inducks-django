<?php

namespace datagutten\InducksORM\models;

use Doctrine\ORM\EntityNotFoundException;
use Doctrine\ORM\Mapping as ORM;

/**
 * EntryJob
 *
 *
 * @author dromanin
 */
#[ORM\Table(name: 'inducks_entryjob')]
#[ORM\Entity(readOnly: true)]
class EntryJob
{
    #[ORM\ManyToOne(targetEntity: Entry::class, inversedBy: 'jobs')]
    #[ORM\JoinColumn(name: 'entrycode', referencedColumnName: 'entrycode')]
    #[ORM\Id]
    private Entry $entry;

    #[ORM\ManyToOne(targetEntity: Person::class, inversedBy: 'entries')]
    #[ORM\JoinColumn(name: 'personcode', referencedColumnName: 'personcode')]
    #[ORM\Id]
    private Person $person;

    /**
     * Describes the job: t=translation, l=lettering, c=colouring
     */
    #[ORM\Column(type: 'string')]
    #[ORM\Id]
    private string $transletcol;

    #[ORM\Column(type: 'string')]
    private string $entryjobcomment;

    public function getEntry(): Entry
    {
        return $this->entry;
    }

    public function getPerson(): Person
    {
        return $this->person;
    }

    public function getTransletcol(): string
    {
        return $this->transletcol;
    }

    public function getEntryjobcomment(): string
    {
        return $this->entryjobcomment;
    }

    public function getRoleName(): string
    {
        switch ($this->transletcol)
        {
            case 'l':
                return 'letterer';
            case 't':
                return 'translator';
            case 'c':
                return 'colorist';
        }
        throw new EntityNotFoundException('Invalid role');
    }

}
