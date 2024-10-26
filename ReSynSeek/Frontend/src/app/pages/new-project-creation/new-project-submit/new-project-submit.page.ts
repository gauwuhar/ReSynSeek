import { Component } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { RouterModule } from '@angular/router';


@Component({
  selector: 'app-new-project-submit',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './new-project-submit.page.html',
  styleUrl: './new-project-submit.page.sass'
})
export class NewProjectSubmitComponent {
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
