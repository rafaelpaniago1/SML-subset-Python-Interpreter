(fn x => fn y => x + y) 3 2

(* Função de alta ordem *)
let compose <- fn f => fn g => fn x => f (g x) in
let double <- fn x => x * 2 in
let increment <- fn x => x + 1 in
(compose double increment) 5
end end end