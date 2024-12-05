import { Component } from '@angular/core';
import { WelcomeLogoComponent } from '../create-log-in-account/logo-animation-account/welcome-logo.page';
import { SignupComponent } from '../create-log-in-account/sign-up-account/signup.page';
import { FooterComponent } from '../../components/footer/footer.component';
import { Router, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-registration-page',
  standalone: true,
  imports: [WelcomeLogoComponent, SignupComponent, FooterComponent, RouterOutlet],
  templateUrl: './registration-page.component.html',
  styleUrl: './registration-page.component.sass'
})
export class RegistrationPageComponent {


}
