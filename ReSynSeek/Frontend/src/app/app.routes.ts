import { Routes } from '@angular/router';
import { LoginPage } from "./pages/login/login.page";
import { ScientificInterestsPage } from "./pages/scientific-interests/scientific-interests.page";
import { BackgroundInformationPage } from "./pages/users/background-information/background-information.page";
import { UserNavPage } from "./pages/users/user-nav/user-nav.page";
import { AboutMePage } from "./pages/users/about-me/about-me.page";

export const routes: Routes = [
  {
    path: 'login',
    component: LoginPage
  },
  {
    path: 'scientific-interests',
    component: ScientificInterestsPage
  },
  {
    path: 'background-information',
    component: BackgroundInformationPage
  },
  {
    path: 'user-nav',
    component: UserNavPage,
  },
  {
    path: 'about-me',
    component: AboutMePage,
  }
];
