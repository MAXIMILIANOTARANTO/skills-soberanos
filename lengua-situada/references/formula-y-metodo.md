# Formula y metodo

Softmax no se toca.

p_i = exp(z_i) / sum_j exp(z_j)

c = (c_hilo, m, F, pi, mu, s)

- m memoria de criterio del hilo
- F marco o sistema de ideas
- pi paradigma
- mu ruta de metodo (cuanti, cuali, mixto) o tipo de dialogo
- s tiempo, lugar, registro, cuerpo

z_k = z(w, c_hilo, m, F, pi, mu, s, k)

p(w,k|c) = softmax(z_k - lambda u_k + gamma h(m,F))

No colapsar k si max p(k) < tau.

Attention(Q,K,V; s,m,F,pi) = softmax(QK^T/sqrt(d) + M(s) + H(m,F,pi)) V

Tres capas de uso — frecuencia del archivo, origen o antiguedad, criterio del hilo. No fundirlas.

Conclusion — no es etapa 1. Si hay procedimiento, llega al final del intercambio o no llega.
