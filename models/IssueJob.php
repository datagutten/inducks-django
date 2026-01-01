<?php

namespace datagutten\InducksORM\models;

use Doctrine\ORM\EntityNotFoundException;
use Doctrine\ORM\Mapping as ORM;

/**
 * IssueJob
 *
 *
 * @author datagutten
 */
#[ORM\Table(name: 'inducks_issuejob')]
#[ORM\Entity(readOnly: true)]
class IssueJob
{
    public function __construct(
        #[ORM\Id, ORM\Column(type: 'string')]
        private string $issuecode,
        #[ORM\Id, ORM\Column(type: 'string')]
        private string $personcode,
    )
    {
    }

    #[ORM\ManyToOne(targetEntity: Issue::class, inversedBy: 'jobs')]
    #[ORM\JoinColumn(name: 'issuecode', referencedColumnName: 'issuecode')]
    private Issue $issue;

    #[ORM\ManyToOne(targetEntity: Person::class, inversedBy: 'issueJobs')]
    #[ORM\JoinColumn(name: 'personcode', referencedColumnName: 'personcode')]
    private Person $person;

    /**
     * Describes the job: t=translation, l=lettering, c=colouring
     */
    #[ORM\Column(type: 'string')]
    #[ORM\Id]
    private string $inxtransletcol;

    #[ORM\Column(type: 'string')]
    private string $issuejobcomment;

    public function getIssue(): Issue
    {
        return $this->issue;
    }

    public function getPerson(): Person
    {
        return $this->person;
    }

    public function getInxtransletcol(): string
    {
        return $this->inxtransletcol;
    }

    public function getEntryjobcomment(): string
    {
        return $this->issuejobcomment;
    }

    public function getRole(): string
    {
        return $this->inxtransletcol;
    }

    public function getRoleName(): string
    {
        switch ($this->inxtransletcol)
        {
            case 'i':
                return 'indexer';
            case 't':
                return 'translator';
            case 'c':
                return 'colorist';
        }
        throw new EntityNotFoundException('Invalid role');
    }

    /**
     * @return string
     */
    public function getIssuecode(): string
    {
        return $this->issuecode;
    }

    /**
     * @return string
     */
    public function getPersoncode(): string
    {
        return $this->personcode;
    }

}
