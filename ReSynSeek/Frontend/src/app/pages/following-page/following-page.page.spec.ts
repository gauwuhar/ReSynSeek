import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FollowingPagePage } from './following-page.page.js';

describe('FollowingPagePage', () => {
  let component: FollowingPagePage;
  let fixture: ComponentFixture<FollowingPagePage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FollowingPagePage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FollowingPagePage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
