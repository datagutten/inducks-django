<?php


use datagutten\InducksORM\models\HeroCharacter;
use datagutten\InducksORM\models\Story;
use Doctrine\Common\Collections\Criteria;
use PHPUnit\Framework\TestCase;

class StoryTest extends TestCase
{
    public function testGetHero()
    {
        $story = InducksORMBootstrap()->find(Story::class, 'D 91048');
        $this->assertEquals('US', $story->getHero()->getCharactercode());
    }

    public function testGetHero2()
    {
        /**
         * @var HeroCharacter $herochar
         */
        $herochar = InducksORMBootstrap()->find(HeroCharacter::class, 'D 91048');
        $this->assertEquals('US', $herochar->getCharacterCode());
        $this->assertEquals('Home By The Sea', $herochar->getStory()->getTitle());
    }

    public function testReferenceTo()
    {
        $story = InducksORMBootstrap()->find(Story::class, 'W OS  456-02');
        $references = $story->getReferencesTo();
        $story = $references->matching(Criteria::create()->where(Criteria::expr()->eq('fromstorycode', 'AR 113')));
        $this->assertEquals('Last sled to Dawson', $story->first()->getFromStory()->getTitle());
    }

    public function testHeader()
    {
        $story = InducksORMBootstrap()->find(Story::class, 'D 91048');
        $headers = $story->getHeaders()->getValues();
        $this->assertEquals('Denmark', $story->getHeader()->getTitle());
    }
}
