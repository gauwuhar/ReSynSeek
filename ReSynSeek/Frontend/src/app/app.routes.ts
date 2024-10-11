import { Routes } from '@angular/router';
import { LoginComponent } from "./components/login/login.component";
import { SignupComponent } from "./components/signup/signup.component";
import { WelcomeLogoComponent } from "./components/welcome-logo/welcome-logo.component";
import { CongratulationsPopupComponent } from "./components/congratulations-popup/congratulations-popup.component";
import { ProjectsFeedComponent } from "./components/projects-feed/projects-feed.component";
import { ProjectProfileComponent } from './components/project-profile/project-profile.component';
import { ScientificInterestsPage } from "./pages/scientific-interests/scientific-interests.page";
import { BackgroundInformationPage } from "./pages/users/background-information/background-information.page";
import { UserNavPage } from "./pages/users/user-nav/user-nav.page";
import { AboutMePage } from "./pages/users/about-me/about-me.page";
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { PersonalInfoEditComponent } from './components/personal-info-edit/personal-info-edit.component';
import { HeaderLoginedComponent } from './components/header-logined/header-logined.component';
import { FollowingPageComponent } from './components/following-page/following-page.component';
import { CreatingProjectComponent } from './components/creating-project/creating-project.component';
import { AboutUsComponent } from './about-us/about-us.component';
import { LoginAndSecurityComponent } from './login-and-security/login-and-security.component';
import { MyProjectsComponent } from './my-projects/my-projects.component';
import { FAQComponent } from './faq/faq.component';
import { ProfileComponent } from './components/profile/profile.component';

export const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'signup',
    component: SignupComponent
  },
  {
    path: 'background-information',
    component: BackgroundInformationPage
  },
  {
    path: 'profile',
    component: ProfileComponent
  },
  {
    path: 'welcome-logo',
    component: WelcomeLogoComponent
  },
  {
    path: 'congratulations-popup',
    component: CongratulationsPopupComponent
  },
  {
    path: 'projects-feed',
    component: ProjectsFeedComponent
  },
  {
    path: 'project-profile',
    component: ProjectProfileComponent
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
  },
  {
    path: 'header',
    component: HeaderComponent
  },
  {
    path: 'footer',
    component: FooterComponent
  },
  {
    path: 'personal-info-edit',
    component: PersonalInfoEditComponent
  },
  {
    path: 'header-logined',
    component: HeaderLoginedComponent
  },
  {
    path: 'following-page',
    component: FollowingPageComponent
  },
  {
    path: 'creating-project',
    component: CreatingProjectComponent
  },
  {
    path: 'about-us',
    component: AboutUsComponent
  },
  {
    path: 'login-and-security',
    component: LoginAndSecurityComponent
  },
  {
    path: 'my-projects',
    component: MyProjectsComponent
  },
  {
    path: 'faq',
    component: FAQComponent
  },
  {
    path: 'profile',
    component: ProfileComponent
  }

];
