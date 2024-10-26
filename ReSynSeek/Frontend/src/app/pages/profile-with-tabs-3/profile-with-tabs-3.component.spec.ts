import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileWithTabs3Component } from './profile-with-tabs-3.component';

describe('ProfileWithTabs3Component', () => {
  let component: ProfileWithTabs3Component;
  let fixture: ComponentFixture<ProfileWithTabs3Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProfileWithTabs3Component]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProfileWithTabs3Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
