import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileWithTabs2Component } from './profile-with-tabs-2.component';

describe('ProfileWithTabs2Component', () => {
  let component: ProfileWithTabs2Component;
  let fixture: ComponentFixture<ProfileWithTabs2Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProfileWithTabs2Component]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProfileWithTabs2Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
