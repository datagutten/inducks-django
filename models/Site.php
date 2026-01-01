<?php

namespace datagutten\InducksORM\models;

use Doctrine\ORM\Mapping as ORM;

/**
 * Site
 *
 *
 * @author dromanin
 */
#[ORM\Table(name: 'inducks_site')]
#[ORM\Entity(readOnly: true)]
class Site
{
    #[ORM\Column(type: 'string')]
    #[ORM\Id]
    private string $sitecode;

    #[ORM\Column(type: 'string')]
    private string $urlbase;
    #[ORM\Column(type: 'string')]
    private string $images;
    #[ORM\Column(type: 'string')]
    private string $sitename;
    #[ORM\Column(type: 'string')]
    private string $sitelogo;
    #[ORM\Column(type: 'string')]
    private string $properties;


    public function getSiteCode(): string
    {
        return $this->sitecode;
    }

    public function getURLBase(): string
    {
        if (str_contains($this->urlbase, 'outducks'))
            return sprintf('https://inducks.org/hr.php?normalsize=1&image=%s', urlencode($this->urlbase));
        else
            return $this->urlbase;
    }

    public function hasImages(): bool
    {
        return $this->images == 'Y';
    }

    public function getSitename(): string
    {
        return $this->sitename;
    }

    public function getSitelogo(): string
    {
        return $this->sitelogo;
    }

    public function getProperties(): string
    {
        return $this->properties;
    }


}
