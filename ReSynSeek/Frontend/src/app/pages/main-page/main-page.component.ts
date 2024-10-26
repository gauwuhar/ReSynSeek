import { Component } from '@angular/core';
import { HeaderComponent } from '../../components/header/header.component';
import { AboutUsComponent } from '../about-synseek/about-us/about-us.page';
import { FooterComponent } from '../../components/footer/footer.component';
import { RouterOutlet } from '@angular/router';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-main-page',
  standalone: true,
  imports: [HeaderComponent, AboutUsComponent, FooterComponent, RouterOutlet],
  templateUrl: './main-page.component.html',
  styleUrl: './main-page.component.sass'
})
export class MainPageComponent {
  
}
