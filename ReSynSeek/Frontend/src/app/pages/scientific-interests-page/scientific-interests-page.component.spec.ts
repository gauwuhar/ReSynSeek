import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ScientificInterestsPageComponent } from './scientific-interests-page.component';

describe('ScientificInterestsPageComponent', () => {
  let component: ScientificInterestsPageComponent;
  let fixture: ComponentFixture<ScientificInterestsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ScientificInterestsPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ScientificInterestsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
