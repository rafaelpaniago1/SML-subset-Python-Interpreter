let
  sqr <- fn x => x * x
in
  let
    twice <- fn a => fn b => a (a b)
  in
    (twice sqr) 3
  end
end