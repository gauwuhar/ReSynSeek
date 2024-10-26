import { ApplicationConfig, provideZoneChangeDetection, isDevMode } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideHttpClient } from '@angular/common/http';
import { TranslocoHttpLoader } from './transloco-loader';
import { provideTransloco } from '@jsverse/transloco';
import { withInMemoryScrolling } from '@angular/router';

export const routerConfig = provideRouter(routes, 
  withInMemoryScrolling({
    scrollPositionRestoration: 'enabled', // Восстановление позиции прокрутки
    anchorScrolling: 'enabled', // Прокрутка по якорям
  })
);


export const appConfig: ApplicationConfig = {
  providers: [provideZoneChangeDetection({ eventCoalescing: true }), provideRouter(routes), provideHttpClient(), provideTransloco({
        config: {
          availableLangs: ['en', 'ru', 'kz'],
          defaultLang: 'en',
          // Remove this option if your application doesn't support changing language in runtime.
          reRenderOnLangChange: true,
          prodMode: !isDevMode(),
        },
        loader: TranslocoHttpLoader
      })]
};
