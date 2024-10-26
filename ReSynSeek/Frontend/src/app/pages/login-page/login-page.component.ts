import { Component } from '@angular/core';
import { LoginComponent } from "../create-log-in-account/log-in-account/login.page";
import { WelcomeLogoComponent } from "../create-log-in-account/logo-animation-account/welcome-logo.page";
import { FooterComponent } from '../../components/footer/footer.component';
import { RouterOutlet } from '@angular/router';


@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [LoginComponent, WelcomeLogoComponent, FooterComponent, RouterOutlet],
  templateUrl: './login-page.component.html',
  styleUrl: './login-page.component.sass'
})
export class LoginPageComponent {
 
}
