import { ApplicationConfig, provideZoneChangeDetection, isDevMode } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { TranslocoHttpLoader } from './transloco-loader';
import { provideTransloco } from '@jsverse/transloco';
import { provideAnimations } from '@angular/platform-browser/animations';
import { loggerInterceptor } from './logger.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [provideZoneChangeDetection({ eventCoalescing: true }), provideAnimations(), provideRouter(routes), provideHttpClient(), provideTransloco({
        config: {
          availableLangs: ['en', 'ru', 'kz'],
          defaultLang: 'en',
          // Remove this option if your application doesn't support changing language in runtime.
          reRenderOnLangChange: true,
          prodMode: !isDevMode(),
        },
        loader: TranslocoHttpLoader
      }),
        provideHttpClient(withInterceptors([
          loggerInterceptor
        ]))]
};
