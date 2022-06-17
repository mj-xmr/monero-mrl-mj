

GAMMA_SHAPE = 19.28
GAMMA_SCALE = (1/1.61)
CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE =             10
DIFFICULTY_TARGET_V2  =                          120  # // seconds
DIFFICULTY_TARGET_V1  =                          60   # // seconds - before first fork
DEFAULT_UNLOCK_TIME = (CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE * DIFFICULTY_TARGET_V2)
RECENT_SPEND_WINDOW = (15 * DIFFICULTY_TARGET_V2)
uint64_t_MAX = 18446744073709551615
MIN_RCT_LENGTH = CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE + 1




gen_rct_outputs <- function(mul) {
  start = 1
  start:(floor(MIN_RCT_LENGTH * mul) + start)
}

mul = 1e5

rct_outputs = gen_rct_outputs(mul)
rct_offsets <- rct_outputs


#self.THROW_WALLET_EXCEPTION_IF(len(rct_offsets) <= decoy_consts.CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE, "error::wallet_internal_error", "Bad offset calculation")

blocks_in_a_year = as.integer(86400 * 365 / DIFFICULTY_TARGET_V2)
#print("blocks_in_a_year", blocks_in_a_year)
#raise IOError("B;")
blocks_to_consider = min(c(length(rct_offsets), blocks_in_a_year))
if (blocks_to_consider < length(rct_offsets)) {
  outputs_to_consider_subtract <- rct_offsets[length(rct_offsets) - blocks_to_consider - 1]
} else {
  outputs_to_consider_subtract <- 0
}

outputs_to_consider = rct_offsets[length(rct_offsets)] - outputs_to_consider_subtract

begin = 0 # rct_offsets.data();
# end = rct_offsets.data() + rct_offsets.size() - CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE;
end = begin + length(rct_offsets) - CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE
#num_rct_outputs = *(end - 1);
num_rct_outputs = rct_offsets[end - 1]
#self.THROW_WALLET_EXCEPTION_IF(self.num_rct_outputs == 0, "error::wallet_internal_error", "No rct outputs");
average_output_time = DIFFICULTY_TARGET_V2 * blocks_to_consider / as.numeric(outputs_to_consider); # // this assumes constant target over the whole rct range



rand_idx <- function(maxVal) {
  sample.int(maxVal, size = 1)
}


lower_bound <- function(iterable, val_to_find) {
  i = findInterval(val_to_find, iterable) # TODO: unclear if rightmost.closed should be TRUE or FALSE
  if (i != length(iterable)) {
    return(i)
  } else {
    return(-1)
  }
}

# def THROW_WALLET_EXCEPTION_IF(self, cond, context, msg):
#   if cond:
#   raise Exception(context + ": " + msg)


pick_n_values_ratio <- function(n) {
  good = 0
  for (i in 0:n) {
    val = pick()
    if (val != uint64_t_MAX) {
      good <- good + 1
    }
    good / n
  }
}

# TODO: Doesnt this pick n + 1 values?
pick_n_values <- function(n) {
  ret <- vector(length = n + 1)
  for (i in 1:(n + 1)) {
    val <- pick()
    if (val != uint64_t_MAX) {
      ret[i] <- val
    }
  }
  ret
}


pick <- function() {
  x = rgamma(1, shape = GAMMA_SHAPE, scale = GAMMA_SCALE)
  x = exp(x)
  if (x > DEFAULT_UNLOCK_TIME) {
    x <- x - DEFAULT_UNLOCK_TIME
  } else {
    x <- rand_idx(RECENT_SPEND_WINDOW)
  }
  
  # output_index = as.integer(x / average_output_time)
  output_index = as.numeric(x / average_output_time)
  
  if (output_index >= num_rct_outputs) {
    return(uint64_t_MAX) # bad pick
  }
  #output_index = self.num_rct_outputs - output_index; # TODO: Altered
  output_index_pre = output_index
  output_index = num_rct_outputs - 1 - output_index # Original
  
  index = lower_bound(rct_offsets[begin:end], output_index)
  
  if (index < 0) {
    # TODO: This was added!
    print(paste0("output_index of ", output_index, " not found, pre = ", output_index_pre, ", num_rct = ", num_rct_outputs))
    print(paste0("Begin", begin, ", end", end))
    print(rct_offsets[begin:end])
  }
  #return decoy_consts.uint64_t_MAX # // bad pick
  # self.THROW_WALLET_EXCEPTION_IF(index < 0, "error::wallet_internal_error", "output_index of {} not found".format(output_index))
  
  # TODO: I changed this to deal with 0-1 indexing change. Double-check that it is correct
  if (index == 1) {
    first_rct = 1
  } else {
    first_rct <- rct_offsets[index - 1]
  }
  n_rct = rct_offsets[index] - first_rct
  if (n_rct == 0) {
    return(uint64_t_MAX) # // bad pick
  }
  #MTRACE("Picking 1/" << n_rct << " in block " << index);
  first_rct + rand_idx(n_rct)
}







n.picks <- 1000000
set.seed(314)

picked.values <- vector(length = n.picks)

for (pick.iter in 1:n.picks) {
  picked.values[pick.iter] <- pick()
}

cat(formatC(picked.values[picked.values != uint64_t_MAX], format = "d"), 
  file = paste0("picks_raw_R_mul_length_", formatC(mul, format = "d"), ".csv"), sep = "\n")


