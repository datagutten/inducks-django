<?php


use datagutten\InducksORM\models\Issue;
use PHPUnit\Framework\TestCase;

class IssueTest extends TestCase
{
    public function setUp(): void
    {
        $this->em = InducksORMBootstrap();
        $this->issue = InducksORMBootstrap()->find(Issue::class, 'no/HOF   5');
    }

    public function testGetThumbnailUrl()
    {
        $url = $this->issue->getThumbnailUrl();
        $this->assertEquals('https://inducks.org/hr.php?normalsize=1&image=https%3A%2F%2Foutducks.org%2Fno%2Fhof/no_hof_005a_001.jpg', $url);
    }

    public function testGetIndexers()
    {
        $issue = $this->em->find(Issue::class, 'no/DP   22');
        $indexers = $issue->getIndexers();
        $this->assertEquals('FAa', $indexers[0]->getPersoncode());
        $this->assertEquals('SGr', $indexers[1]->getPersoncode());
    }

//    public function testStories()
//    {
//        $issue = $this->em->find(Issue::class, 'no/DP   22');
//    }
}
