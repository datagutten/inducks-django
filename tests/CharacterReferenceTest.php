<?php

use PHPUnit\Framework\TestCase;


class CharacterReferenceTest extends TestCase
{
    public function testReferencesFrom()
    {
        $character = InducksORMBootstrap()->find(\datagutten\InducksORM\models\Character::class, 'DD');
        $references = $character->getReferencesFrom();
        $character_ref = InducksORMBootstrap()->find(\datagutten\InducksORM\models\Character::class, 'YDD');
        $this->assertTrue($references->contains($character_ref));
        //$this->assertContains($character_ref, $references);
    }
}
