let
  sqr <- fn x => x * x
in
  let
    twice <- fn a => fn b => a (a b)
  in
    (twice sqr) 3
  end
end

(* Função recursiva avançada *)
fun power base exp =>
  if exp <= 0 then 1
  else base * power base (exp - 1)

(* Combinação de let e fun *)
let
  factorial <- fun fact n =>
    if n <= 1 then 1
    else n * fact (n - 1)
in
  factorial 6
end