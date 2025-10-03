fun fibonacci n =>
  if n <= 1 then n
  else fibonacci (n - 1) + fibonacci (n - 2)

fun power base exp =>
  if exp = 0 then 1
  else base * power base (exp - 1)

fun sum_range start finish =>
  if start > finish then 0
  else start + sum_range (start + 1) finish

let result <- fibonacci 7 in
  let pow_result <- power 2 4 in
    let sum_result <- sum_range 1 10 in
      result + pow_result + sum_result
    end
  end
end