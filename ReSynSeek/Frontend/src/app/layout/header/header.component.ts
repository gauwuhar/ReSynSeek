import { Component } from '@angular/core';
import { RouterLink } from "@angular/router";
import { TranslocoPipe } from "@jsverse/transloco";

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    RouterLink,
    TranslocoPipe
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.sass'
})
export class HeaderComponent {

}
