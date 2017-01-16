// $Id: HandMatchupTest.java 384 2004-05-11 06:27:47Z mjmaurer $

package org.pokersource.enumerate.test;

import junit.framework.TestCase;
import org.pokersource.enumerate.HandMatchup;

/**
 @author Michael Maurer &lt;<a href="mailto:mjmaurer@yahoo.com">mjmaurer@yahoo.com</a>&gt;
 */

public class HandMatchupTest extends TestCase {
  HandMatchup hm1;
  HandMatchup hm2;
  HandMatchup hm3;
  HandMatchup hm4;

  public HandMatchupTest(String name) {
    super(name);
  }

  public static void main(String args[]) {
    junit.textui.TestRunner.run(HandMatchupTest.class);
  }

  protected void setUp() {
    hm1 = new HandMatchup(new long[]{1, 2, 3, 4});
    hm2 = new HandMatchup(new long[]{1, 2, 3, 4});
    hm3 = new HandMatchup(new long[]{6, 7, 8, 9});
    hm4 = new HandMatchup(new long[]{1, 2, 3});
  }

  public void testEquals() {
    assertTrue(hm1.equals(hm1));
    assertTrue(hm1.equals(hm2));
    assertTrue(!hm1.equals(hm3));
    assertTrue(!hm1.equals(hm4));

    assertTrue(hm2.equals(hm1));
    assertTrue(hm2.equals(hm2));
    assertTrue(!hm2.equals(hm3));
    assertTrue(!hm2.equals(hm4));

    assertTrue(!hm3.equals(hm1));
    assertTrue(!hm3.equals(hm2));
    assertTrue(hm3.equals(hm3));
    assertTrue(!hm3.equals(hm4));

    assertTrue(!hm4.equals(hm1));
    assertTrue(!hm4.equals(hm2));
    assertTrue(!hm4.equals(hm3));
    assertTrue(hm4.equals(hm4));
  }

  public void testHashCode() {
    assertTrue(hm1.hashCode() == hm1.hashCode());
    assertTrue(hm1.hashCode() == hm2.hashCode());
    assertTrue(hm1.hashCode() != hm3.hashCode());
    assertTrue(hm1.hashCode() != hm4.hashCode());

    assertTrue(hm2.hashCode() == hm1.hashCode());
    assertTrue(hm2.hashCode() == hm2.hashCode());
    assertTrue(hm2.hashCode() != hm3.hashCode());
    assertTrue(hm2.hashCode() != hm4.hashCode());

    assertTrue(hm3.hashCode() != hm1.hashCode());
    assertTrue(hm3.hashCode() != hm2.hashCode());
    assertTrue(hm3.hashCode() == hm3.hashCode());
    assertTrue(hm3.hashCode() != hm4.hashCode());

    assertTrue(hm4.hashCode() != hm1.hashCode());
    assertTrue(hm4.hashCode() != hm2.hashCode());
    assertTrue(hm4.hashCode() != hm3.hashCode());
    assertTrue(hm4.hashCode() == hm4.hashCode());
  }

}

