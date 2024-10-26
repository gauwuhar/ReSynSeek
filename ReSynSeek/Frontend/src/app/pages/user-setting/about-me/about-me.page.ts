import { Component, OnInit } from '@angular/core';
import { UserService } from "../../../services/user.service";
import { AboutMeModel } from "../../../model/about-me.model";

@Component({
  selector: 'app-about-me',
  standalone: true,
  imports: [],
  templateUrl: './about-me.page.html',
  styleUrl: './about-me.page.sass'
})
export class AboutMePage implements OnInit{

  aboutMe?: AboutMeModel;

  constructor(
    private userService: UserService,
  ) {
  }

  ngOnInit() {
    this.aboutMe = this.userService.getAboutMe();
  }

}
