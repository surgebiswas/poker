// $Id: NestedLoopSampling.java 384 2004-05-11 06:27:47Z mjmaurer $

package org.pokersource.util;

import java.util.Enumeration;
import java.util.Random;

/** Like NestedLoopEnumeration, but rather than visiting every entry in
 turn, randomly samples with replacement.
 @see NestedLoopEnumeration
 @author Michael Maurer &lt;<a href="mailto:mjmaurer@yahoo.com">mjmaurer@yahoo.com</a>&gt;
 */

public class NestedLoopSampling implements Enumeration {
  private int nsamples;
  private int[] elem;       // a copy of the next element we return in next()
  private int[] limits;     // loop limits for each dimension
  private Random rand;

  /** Initializes a nested loop sampler with limits.length dimensions.
   @param limits limits[i] is the upper limit of the ith nested loop (the
   loop runs from 0 to limits[i]-1 inclusive)
   @param nsamples the number of samples to generate before
   hasMoreElements() returns false
   */
  public NestedLoopSampling(int[] limits, int nsamples) {
    if (nsamples <= 0)
      throw new IllegalArgumentException("nsamples must be positive");
    for (int i = 0; i < limits.length; i++) {
      if (limits[i] <= 0)
        throw new IllegalArgumentException("limits must be positive");
    }
    this.nsamples = nsamples;
    this.limits = limits;
    elem = new int[limits.length];
    rand = new Random();
  }

  public NestedLoopSampling(int[] limits) {
    this(limits, Integer.MAX_VALUE);
  }

  public boolean hasMoreElements() {
    return nsamples > 0;
  }

  /** Return an integer array sampling the next loop indices for each
   dimension.
   @return An object of int[] type; the ith value is the loop variable
   for the ith nested loop.
   */
  public Object nextElement() {
    if (nsamples == 0)
      return null;
    for (int i = 0; i < limits.length; i++)
      elem[i] = rand.nextInt(limits[i]);
    nsamples--;
    return elem;
  }
}
