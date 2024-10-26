import { Component } from '@angular/core';
import { HeaderLoginedComponent } from "../../components/header-logined/header-logined.component";
import { AboutMePage } from "../user-setting/about-me/about-me.page";
import { ProjectProfileComponent } from "../project-profile/project-profile.page";
import { ProfileComponent } from "../user-profile/profile-header/profile.page";
import { ProfileInformationComponent } from "../profile-information/profile-information.component";
import { FooterComponent } from "../../components/footer/footer.component";
import { RouterOutlet } from '@angular/router';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-profile-with-tabs-1',
  standalone: true,
  imports: [HeaderLoginedComponent, AboutMePage, ProjectProfileComponent, ProfileComponent, ProfileInformationComponent, FooterComponent, RouterOutlet],
  templateUrl: './profile-with-tabs-1.component.html',
  styleUrl: './profile-with-tabs-1.component.sass'
})
export class ProfileWithTabs1Component {
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
