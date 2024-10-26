import { Component } from '@angular/core';
import { HeaderLoginedComponent } from "../../components/header-logined/header-logined.component";
import { ProfileComponent } from "../user-profile/profile-header/profile.page";
import { FollowingPagePage } from "../following-page/following-page.page";
import { FooterComponent } from "../../components/footer/footer.component";
import { RouterOutlet } from '@angular/router';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-profile-with-tabs-3',
  standalone: true,
  imports: [HeaderLoginedComponent, ProfileComponent, FollowingPagePage, FooterComponent, RouterOutlet],
  templateUrl: './profile-with-tabs-3.component.html',
  styleUrl: './profile-with-tabs-3.component.sass'
})
export class ProfileWithTabs3Component {
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
