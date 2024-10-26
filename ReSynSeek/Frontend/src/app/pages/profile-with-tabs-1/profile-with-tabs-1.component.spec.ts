import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileWithTabs1Component } from './profile-with-tabs-1.component';

describe('ProfileWithTabs1Component', () => {
  let component: ProfileWithTabs1Component;
  let fixture: ComponentFixture<ProfileWithTabs1Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProfileWithTabs1Component]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProfileWithTabs1Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
