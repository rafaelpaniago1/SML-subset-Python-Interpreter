let 
  one <- 1
in
  let
    f <- fn x => x + one
  in
    let
      one <- 2
    in
      f 5
    end
  end
end