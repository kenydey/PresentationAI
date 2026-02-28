import React from "react";
import Header from "../dashboard/components/Header";
import Wrapper from "@/components/Wrapper";

const ProfilePage = async () => {
  return (
    <div className="min-h-screen bg-[#E9E8F8]">
      <Header />

      <Wrapper className="lg:w-[60%]">
        <div className="py-8 space-y-6">
          {/* Profile Details Section */}
          <div className="bg-white rounded-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-medium text-[#101828]">
                Profile Detail
              </h2>
            </div>
          </div>
        </div>
      </Wrapper>
    </div>
  );
};

export default ProfilePage;
