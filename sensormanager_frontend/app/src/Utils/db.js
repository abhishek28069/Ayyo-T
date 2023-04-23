import { createClient } from "@supabase/supabase-js";

const url = "https://zakntpuxbdegdkyvdzkw.supabase.co";
const key =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpha250cHV4YmRlZ2RreXZkemt3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODEyODIyNjEsImV4cCI6MTk5Njg1ODI2MX0.qJp48cSwfb0QKFOE-TAB22yJN_m6rU6kK5Ers_GgcHM";

export const supabase = createClient(url, key);
