import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginAndSecurityComponent } from './login-and-security.component';

describe('LoginAndSecurityComponent', () => {
  let component: LoginAndSecurityComponent;
  let fixture: ComponentFixture<LoginAndSecurityComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginAndSecurityComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoginAndSecurityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
