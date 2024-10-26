import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreatingProjectKeyInfoPageComponent } from './creating-project-key-info-page.component';

describe('CreatingProjectKeyInfoPageComponent', () => {
  let component: CreatingProjectKeyInfoPageComponent;
  let fixture: ComponentFixture<CreatingProjectKeyInfoPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreatingProjectKeyInfoPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreatingProjectKeyInfoPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
