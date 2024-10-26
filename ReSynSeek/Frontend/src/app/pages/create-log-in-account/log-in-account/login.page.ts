import { Component } from '@angular/core';
import { TranslocoPipe } from "@jsverse/transloco";
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports:
  [
    RouterModule,
    TranslocoPipe
  ],
  templateUrl: './login.page.html',
  styleUrl: './login.page.sass'
})
export class LoginComponent {

}
