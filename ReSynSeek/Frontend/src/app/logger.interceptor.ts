import { HttpInterceptorFn } from '@angular/common/http';

// интерсептор запросов

export const loggerInterceptor: HttpInterceptorFn = (req, next) => {
  console.log(`hello ${req.url}`);
  const authReq = req.clone({
    headers: req.headers.set('Authorization', 'Bearer the token'),
  });
  return next(authReq);
};
