import { Routes } from '@angular/router';
import { LoginComponent } from "./pages/create-log-in-account/log-in-account/login.page";
import { SignupComponent } from './pages/create-log-in-account/sign-up-account/signup.page';
import { WelcomeLogoComponent } from "./pages/create-log-in-account/logo-animation-account/welcome-logo.page";
import { CongratulationsPopupComponent } from "./components/congratulations-popup/congratulations-popup.component";
import { ProjectsFeedComponent } from "./pages/projects-feed/projects-feed.page";
import { ProjectProfileComponent } from "./pages/project-profile/project-profile.page";
import { NewProjectSubmitComponent } from "./pages/new-project-creation/new-project-submit/new-project-submit.page";
import { ScientificInterestsPage } from "./pages/scientific-interests/scientific-interests.page";
import { BackgroundInformationPage } from "./pages/user-setting/background-information/background-information.page";
import { UserNavPage } from "./pages/user-setting/user-nav/user-nav.page";
import { AboutMePage } from "./pages/user-setting/about-me/about-me.page";
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { PersonalInfoEditPage } from './pages/personal-info-edit/personal-info-edit.page';
import { HeaderLoginedComponent } from './components/header-logined/header-logined.component';
import { FollowingPagePage } from './pages/following-page/following-page.page';
import { CreatingProjectTopicPage } from './pages/creating-project-topic/creating-project-topic.page';
import { CreatingProjectKeyInfoPage } from './pages/creating-project-key-info/creating-project-key-info.page';
import { AboutUsComponent } from './pages/about-synseek/about-us/about-us.page';
import { LoginAndSecurityComponent } from './pages/user-setting/login-and-security/login-and-security.page';
import { MyProjectsComponent } from './components/user-profile/my-projects/my-projects.component';
import { FAQComponent } from './pages/FAQ_p/faq/faq.page';
import { ProfileComponent } from './pages/user-profile/profile-header/profile.page';
import { UserSettingsLookingForComponent } from './pages/new-project-creation/user-settings-looking-for/user-settings-looking-for.page';
import { MainPageComponent } from './pages/main-page/main-page.component';
import { RegistrationPageComponent } from './pages/registration-page/registration-page.component';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import { ScientificInterestsPageComponent } from './pages/scientific-interests-page/scientific-interests-page.component';
import { ProfileWithTabs3Component } from './pages/profile-with-tabs-3/profile-with-tabs-3.component';
import { ProfileWithTabs2Component } from './pages/profile-with-tabs-2/profile-with-tabs-2.component';
import { SafetySettingsPageComponent } from './pages/safety-settings-page/safety-settings-page.component';
import { ProjectsFeedPageComponent } from './pages/projects-feed-page/projects-feed-page.component';
import { ProjectProfilePageComponent } from './pages/project-profile-page/project-profile-page.component';
import { CreatingProjectTopicPageComponent } from './pages/creating-project-topic-page/creating-project-topic-page.component';
import { CreatingProjectKeyInfoPageComponent } from './pages/creating-project-key-info-page/creating-project-key-info-page.component';
import { CreatingProjectVacanciesPageComponent } from './pages/creating-project-vacancies-page/creating-project-vacancies-page.component';
import { CreatingProjectSubmitPageComponent } from './pages/creating-project-submit-page/creating-project-submit-page.component';
import { FaqPageComponent } from './pages/faq-page/faq-page.component';
import { ProfileInformationComponent } from './pages/profile-information/profile-information.component';
import { ProfileWithTabs1Component } from './pages/profile-with-tabs-1/profile-with-tabs-1.component';

export const routes: Routes = [


  // Тут собранные страницы
  { path: 'main-page', component: MainPageComponent },
  { path: 'registration-page', component: RegistrationPageComponent },
  { path: 'login-page', component: LoginPageComponent },
  { path: 'scientific-interests-page', component: ScientificInterestsPageComponent },
  { path: 'profile-with-tabs-three', component: ProfileWithTabs3Component },
  { path: 'profile-with-tabs-two', component: ProfileWithTabs2Component },
  { path: 'safety-settings-page', component: SafetySettingsPageComponent },
  { path: 'projects-feed-page', component: ProjectsFeedPageComponent },
  { path: 'project-profile-page', component: ProjectProfilePageComponent },
  { path: 'creating-project-topic-page', component: CreatingProjectTopicPageComponent },
  { path: 'creating-project-key-info-page', component: CreatingProjectKeyInfoPageComponent },
  { path: 'creating-project-vacancies-page', component: CreatingProjectVacanciesPageComponent },
  { path: 'creating-project-submit-page', component: CreatingProjectSubmitPageComponent},
  { path: 'faq-page', component: FaqPageComponent},
  { path: 'profile-with-tabs-one', component: ProfileWithTabs1Component},


  // А тут уже сами компоненты
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'welcome-logo', component: WelcomeLogoComponent },
  { path: 'congratulations-popup', component: CongratulationsPopupComponent },
  { path: 'projects-feed', component: ProjectsFeedComponent },
  { path: 'project-profile', component: ProjectProfileComponent },
  { path: 'new-project-submit', component: NewProjectSubmitComponent },
  { path: 'scientific-interests', component: ScientificInterestsPage },
  { path: 'background-information', component: BackgroundInformationPage },
  { path: 'user-nav', component: UserNavPage },
  { path: 'about-me', component: AboutMePage },
  { path: 'header', component: HeaderComponent },
  { path: 'footer', component: FooterComponent },
  { path: 'personal-info-edit', component: PersonalInfoEditPage },
  { path: 'header-logined', component: HeaderLoginedComponent },
  { path: 'following-page', component: FollowingPagePage },
  { path: 'creating-project-topic', component: CreatingProjectTopicPage },
  { path: 'creating-project-key-info', component: CreatingProjectKeyInfoPage },
  { path: 'about-us', component: AboutUsComponent },
  { path: 'login-and-security', component: LoginAndSecurityComponent },
  { path: 'my-projects', component: MyProjectsComponent },
  { path: 'faq', component: FAQComponent },
  { path: 'user-settings-looking-for', component: UserSettingsLookingForComponent },
  { path: 'profile-information', component: ProfileInformationComponent}
];
