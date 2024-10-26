import { Component } from '@angular/core';
import { HeaderLoginedComponent } from "../../components/header-logined/header-logined.component";
import { LoginAndSecurityComponent } from "../user-setting/login-and-security/login-and-security.page";
import { FooterComponent } from "../../components/footer/footer.component";

@Component({
  selector: 'app-safety-settings-page',
  standalone: true,
  imports: [HeaderLoginedComponent, LoginAndSecurityComponent, FooterComponent],
  templateUrl: './safety-settings-page.component.html',
  styleUrl: './safety-settings-page.component.sass'
})
export class SafetySettingsPageComponent {

}
