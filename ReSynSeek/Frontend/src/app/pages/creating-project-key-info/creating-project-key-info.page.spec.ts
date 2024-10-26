import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreatingProjectKeyInfoPage } from './creating-project-key-info.page';

describe('CreatingProjectKeyInfoPage', () => {
  let component: CreatingProjectKeyInfoPage;
  let fixture: ComponentFixture<CreatingProjectKeyInfoPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreatingProjectKeyInfoPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreatingProjectKeyInfoPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
