import { Component } from '@angular/core';
import { HeaderLoginedComponent } from "../../components/header-logined/header-logined.component";
import { MyProjectsComponent } from "../../components/user-profile/my-projects/my-projects.component";
import { ProfileComponent } from "../user-profile/profile-header/profile.page";
import { FooterComponent } from "../../components/footer/footer.component";
import { RouterOutlet } from '@angular/router';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-profile-with-tabs-2',
  standalone: true,
  imports: [HeaderLoginedComponent, MyProjectsComponent, ProfileComponent, FooterComponent, RouterOutlet],
  templateUrl: './profile-with-tabs-2.component.html',
  styleUrl: './profile-with-tabs-2.component.sass'
})
export class ProfileWithTabs2Component {
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
