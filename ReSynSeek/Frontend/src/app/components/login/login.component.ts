import { Component } from '@angular/core';
import { TranslocoPipe } from "@jsverse/transloco";

@Component({
  selector: 'app-login',
  standalone: true,
  imports:
  [
    TranslocoPipe
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.sass'
})
export class LoginComponent {

}
