<?php

use datagutten\InducksORM\models\Person;
use PHPUnit\Framework\TestCase;


class PersonTest extends TestCase
{

    public function testGetEntries()
    {
        $person = InducksORMBootstrap()->find(Person::class, 'DR');
        $entries = $person->getEntries()->first();
    }
}
