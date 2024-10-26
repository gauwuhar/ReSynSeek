import { Component } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-personal-info-edit',
  standalone: true,
  imports: [],
  templateUrl: './personal-info-edit.page.html',
  styleUrl: './personal-info-edit.page.sass'
})
export class PersonalInfoEditPage {
  constructor(private router: Router) {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        const fragment = this.router.parseUrl(this.router.url).fragment;
        if (fragment) {
          document.getElementById(fragment)?.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  }
}
