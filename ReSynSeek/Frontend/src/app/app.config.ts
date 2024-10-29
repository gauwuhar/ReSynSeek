import { ApplicationConfig, provideZoneChangeDetection, isDevMode } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { TranslocoHttpLoader } from './transloco-loader';
import { provideTransloco } from '@jsverse/transloco';
import { withInMemoryScrolling } from '@angular/router';
import { loggerInterceptor } from './logger.interceptor';
import { errorInterceptor } from './error.interceptor';
import { ReactiveFormsModule } from '@angular/forms'; // Импортируйте ReactiveFormsModule

export const routerConfig = provideRouter(routes,
  withInMemoryScrolling({
    scrollPositionRestoration: 'enabled', // Восстановление позиции прокрутки
    anchorScrolling: 'enabled', // Прокрутка по якорям
  })
);


export const appConfig: ApplicationConfig = {
  providers: [provideZoneChangeDetection({ eventCoalescing: true }), provideRouter(routes), provideHttpClient(withInterceptors([loggerInterceptor, errorInterceptor])), provideTransloco({
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
