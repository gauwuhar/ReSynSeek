import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [RouterModule, RouterOutlet],
  templateUrl: './profile.page.html',
  styleUrl: './profile.page.sass'
})
export class ProfileComponent {

}
