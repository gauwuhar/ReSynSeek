import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WelcomeLogoComponent } from './welcome-logo.component';

describe('WelcomeLogoComponent', () => {
  let component: WelcomeLogoComponent;
  let fixture: ComponentFixture<WelcomeLogoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WelcomeLogoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WelcomeLogoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
