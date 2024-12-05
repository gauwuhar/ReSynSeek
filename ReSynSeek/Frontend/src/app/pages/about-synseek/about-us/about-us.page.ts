import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { RouterModule } from '@angular/router';
import { UserService } from '../../../services/user.service';

@Component({
  selector: 'app-about-us',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './about-us.page.html',
  styleUrl: './about-us.page.sass'
})
export class AboutUsComponent implements OnInit {
  message?: any;
  constructor(private router: Router, private userService: UserService) {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        const fragment = this.router.parseUrl(this.router.url).fragment;
        if (fragment) {
          document.getElementById(fragment)?.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  }
  async ngOnInit() {
    this.message = (await this.userService.getHelloWorld());
    console.log(this.message);
  }
}

